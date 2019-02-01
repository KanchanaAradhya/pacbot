/*******************************************************************************
 * Copyright 2018 T Mobile, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License.  You may obtain a copy
 * of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
 * License for the specific language governing permissions and limitations under
 * the License.
 ******************************************************************************/
package com.tmobile.pacman.api.admin.repository;

import java.util.List;
import java.util.Set;

import javax.transaction.Transactional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.tmobile.pacman.api.admin.repository.model.AssetGroupTargetDetails;

/**
 * AssetGroupTargetDetails Repository Interface
 */
@Repository
public interface AssetGroupTargetDetailsRepository extends JpaRepository<AssetGroupTargetDetails, String> {

	/**
     * AssetGroupTargetDetails Repository function for to get all AssetGroupTarget details by groupId
     *
     * @author Nidhish
     * @param groupId - valid group Id
     * @return All AssetGroupTarget Details
     */
	public List<AssetGroupTargetDetails> findByGroupId(String groupId);

	/**
     * AssetGroupTargetDetails Repository function for to get all AssetGroupTarget details by groupId and targetType not in list
     *
     * @author Nidhish
     * @param groupId - valid group Id
     * @param targetTypes - valid targetTypes list
     * @return All AssetGroupTarget Details
     */
	public List<AssetGroupTargetDetails> findByGroupIdAndTargetTypeNotIn(String groupId, Set<String> targetTypes);

	/**
     * AssetGroupTargetDetails Repository function for to delete all AssetGroupTarget details by groupId
     *
     * @author Nidhish
     * @param groupId - valid group Id
     * @return All deleted AssetGroupTarget Details
     */
    @Transactional
    public List<AssetGroupTargetDetails> deleteByGroupIdIgnoreCase(String groupId);
}




